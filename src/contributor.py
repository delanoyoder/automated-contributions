import requests
import subprocess
from os import chdir
from json import load
from uuid import uuid4
from datetime import datetime
from argparse import ArgumentParser
from paths import BaseDir, ConfigsDir


class Committer:
    def __init__(self, config_name):
        self.load(config_name)

    def load(self, config_name):
        if not config_name.endswith(".json"):
            config_name += ".json"
        config_path = f"{ConfigsDir}/{config_name}"
        with open(config_name, "r") as infile:
            config = load(infile)
        self.username = config["username"]
        self.repository_path = config["repository_path"]
        self.daily_commit_limit = int(config["daily_commit_limit"])
        self.start_date = datetime.strptime(config["start_date"], "%Y-%m-%d").date()
        self.sorted_colored_boxes = config["contributions"]

        with open(f"{BaseDir}/access_token.json", "r") as infile:
            self.access_token = load(infile)

    def daily_check(self):
        today = datetime.now().date()
        days_since_start = (today - self.start_date).days
        row = days_since_start % 7
        column = days_since_start // 7

        if [row, column] in self.sorted_colored_boxes:
            num_contributions = self.get_contributions(today)
            print(f"Today's contributions: {num_contributions}")
            for _ in range(self.daily_commit_limit - num_contributions):
                self.make_contribution(today)

    def get_contributions(self, date):
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        query = """
        query($username: String!, $from: DateTime!, $to: DateTime!) {
            user(login: $username) {
                contributionsCollection(from: $from, to: $to) {
                    contributionCalendar {
                        totalContributions
                    }
                }
            }
        }
        """
        variables = {
            "username": self.username,
            "from": f'{date.strftime("%Y-%m-%d")}T00:00:00Z',
            "to": f'{date.strftime("%Y-%m-%d")}T23:59:59Z',
        }

        response = requests.post(
            url, headers=headers, json={"query": query, "variables": variables}
        )

        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return

        data = response.json()
        collection = data["data"]["user"]["contributionsCollection"]
        contributions = collection["contributionCalendar"]["totalContributions"]

        return contributions

    def make_contribution(self, date):
        commit_message = f"{date}-{uuid4().hex}"
        main_branch_name = self.get_main_branch_name()

        chdir(self.repository_path)
        self.checkout(main_branch_name)
        self.commit(commit_message)
        self.push(main_branch_name)

    @staticmethod
    def get_main_branch_name():
        command = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        return (
            subprocess.run(command, capture_output=True).stdout.decode("utf-8").strip()
        )

    @staticmethod
    def checkout(branch_name):
        subprocess.run(["git", "checkout", branch_name])
        subprocess.run(["git", "fetch"])
        subprocess.run(["git", "pull", "origin", branch_name])

    @staticmethod
    def commit(commit_name):
        with open("dummy_file.txt", "a") as file:
            file.write(f"Commit on {commit_name}\n")
        subprocess.run(["git", "add", "dummy_file.txt"])
        subprocess.run(["git", "commit", "-m", commit_name])

    @staticmethod
    def push(branch_name):
        subprocess.run(["git", "push", "origin", branch_name, "-f"])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, help="Name of configuration file")
    args = parser.parse_args()
    scheduler = Committer(args.config)
    scheduler.daily_check()
