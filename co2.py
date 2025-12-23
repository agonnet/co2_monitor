import gzip
import os
import shutil
from datetime import datetime, timezone
from statistics import mean

from scd4x import SCD4X

from dropbox_upload import upload_to_dropbox


def do_minute_changed(file_prefix, date_time_now, co2, temperature, relative_humidity):
    with open(f"{file_prefix}.csv", "a") as out:
        out.write(f"{date_time_now},{co2},{temperature},{relative_humidity}")


def do_day_changed(file_prefix):
    csv_name = f"{file_prefix}.csv"
    gz_name = f"{file_prefix}.csv.gz"
    # GZIP the csv data
    with open(csv_name, 'rb') as f_in:
        with gzip.open(gz_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    ok = upload_to_dropbox(gz_name)

    if ok:
        os.remove(gz_name)


def get_readings_loop():
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
        if prev_date_time and prev_date_time != date_time_now:
            do_minute_changed(date_now, date_time_now, mean(co2s), mean(temperatures), mean(relative_humidities))
            co2s = []
            temperatures = []
            relative_humidities = []
        if prev_date and prev_date != date_now:
            do_day_changed(prev_date)
        prev_date = date_now
        prev_date_time = date_time_now


if __name__ == '__main__':
    device = SCD4X(quiet=False)
    device.start_periodic_measurement()
    get_readings_loop()
