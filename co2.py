import gzip
import os
import shutil
from datetime import datetime, timezone
from statistics import mean

from scd4x import SCD4X

from dropbox_upload import upload_to_dropbox


def do_minute_changed(file_prefix, date_time_now, n, co2, temperature, relative_humidity):
    with open(f"{file_prefix}.csv", "a") as out:
        out.write(f"{date_time_now},{n},{co2:.2f},{temperature:.2f},{relative_humidity:.2f}\n")


def gzip_csvs(_exclude_prefix):
    for file_name in os.listdir("."):
        if file_name.endswith(".csv") and \
            (_exclude_prefix is None or not file_name.startswith(_exclude_prefix)):
            csv_name = file_name
            gz_name = f"{csv_name}.gz"
            # GZIP the csv data
            with open(csv_name, 'rb') as f_in:
                with gzip.open(gz_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(csv_name)


def upload_gzips(_exclude_prefix):
    for file_name in os.listdir("."):
        if file_name.endswith(".gz") and \
            (_exclude_prefix is None or not file_name.startswith(_exclude_prefix)):
            gz_name = file_name
            ok = upload_to_dropbox(gz_name)
            if ok:
                os.remove(gz_name)


def do_day_changed(_exclude_prefix=None):
    gzip_csvs(_exclude_prefix)
    upload_gzips(_exclude_prefix)


def get_readings_loop(device):
    prev_date = None
    prev_date_time = None
    co2s = []
    temperatures = []
    relative_humidities = []
    while True:
        # Get readings
        co2, temperature, relative_humidity, timestamp = device.measure()
        now = datetime.fromtimestamp(timestamp, timezone.utc)

        # Collate readings
        co2s.append(co2)
        temperatures.append(temperature)
        relative_humidities.append(relative_humidity)

        # Store mean readings every minute and upload every day
        date_now = now.strftime("%Y.%m.%d")
        date_time_now = now.strftime("%Y.%m.%d.%H.%M")
        num_readings = len(co2s)

        # Do date change first as all csvs are zipped and uploaded so don't want new days csv yet
        if prev_date and prev_date != date_now:
            do_day_changed(prev_date)

        if num_readings and prev_date_time and prev_date_time != date_time_now:
            do_minute_changed(date_now, date_time_now, num_readings, mean(co2s), mean(temperatures), mean(relative_humidities))
            co2s = []
            temperatures = []
            relative_humidities = []
        prev_date = date_now
        prev_date_time = date_time_now


def log_started():
    msg = f"restarted at {datetime.now()}"

    print(msg)

    with open(f"restarts.log", "a") as out:
        out.write(f"{msg}\n")

    upload_to_dropbox("restarts.log")


if __name__ == '__main__':
    log_started()

    exclude_prefix = datetime.now().strftime("%Y.%m.%d")
    do_day_changed(exclude_prefix)  # Upload anything not done previously

    device = SCD4X(quiet=False)
    device.start_periodic_measurement()
    get_readings_loop(device)
