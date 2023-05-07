import json
from os import getcwd
import subprocess
from crontab import CronTab
from datetime import datetime, timedelta
from box_grid import BoxGrid
from paths import BaseDir, SrcDir, ConfigsDir


class CommitScheduler:
    def __init__(self):
        self.prompt_user()

    def prompt_user(self):
        contributions = self.set_contribution_calendar()

        username = input("Enter your GitHub username: ")

        access_token = input("Enter your GitHub access token: ")

        repository_path = input("Enter the path to your dummy repository: ")

        daily_commit_limit = input("Enter your daily commit limit: ")
        assert daily_commit_limit.isdigit(), "Daily commit limit must be an integer."

        start_date = input("Enter your start date (YYYY-MM-DD): ")
        start_date = self.valid_start_date(start_date)

        time_of_day = input("Enter the time of day you want to commit (HH:MM): ")
        if ":" not in time_of_day:
            print("Invalid time of day format.")
            time_of_day = "19:59"
            print(f"Defaulting to {time_of_day}.")

        config_name = input("Enter the name of your configuration: ")
        if not config_name.endswith(".json"):
            config_name += ".json"
        config_name = f"{ConfigsDir}/{config_name}"

        self.create_config_file(
            config_name=config_name,
            username=username,
            repository_path=repository_path,
            daily_commit_limit=daily_commit_limit,
            start_date=start_date,
            time_of_day=time_of_day,
            contributions=contributions,
        )
        self.create_access_token_file(access_token)
        self.create_cron_job(config_name, time_of_day)

        subprocess.run(["python", f"{SrcDir}/display.py", "--config", config_name])
        print("Configuration complete.")

    def set_contribution_calendar(self):
        box_grid = BoxGrid(7, 52)
        box_grid.mainloop()
        return sorted(box_grid.get_clicked_boxes())

    def valid_start_date(self, start_date):
        date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if date.weekday() != 6:
            print("Your start date needs to be a Sunday.")
            days_to_add = 6 - date.weekday()
            date += timedelta(days=days_to_add)
            print(f"The next Sunday is {date}, which will be your start date.")
            start_date = date.strftime("%Y-%m-%d")
        return start_date

    def create_config_file(self, **kwargs):
        with open(kwargs["config_name"], "w") as f:
            json.dump(kwargs, f)

    def create_access_token_file(self, access_token):
        with open(f"{BaseDir}/access_token.json", "w") as f:
            json.dump(access_token, f)

    def create_cron_job(self, config, time_of_day):
        cron = CronTab(user=True)
        command = "/bin/bash -c '"
        command += f"echo $(date); "
        command += f"source {BaseDir}/venv/bin/activate; "
        command += f"python {SrcDir}/contributor.py "
        command += f"--config {config}' "
        command += f">> {BaseDir}/cron.log 2>&1"
        job = cron.new(command=command)
        hour, minute = time_of_day.split(":")
        job.setall(f"{minute} {hour} * * *")
        cron.write()


if __name__ == "__main__":
    commit_scheduler = CommitScheduler()
