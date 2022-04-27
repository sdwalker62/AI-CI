commit_steps = [
    "clone_repository", 
    "python_version", 
    "black_formatter", 
    "sphinx", 
    "discord_notifier",
    "formatting-finished", #Type of message to send for above discord notifier
    "snyk_analysis",
    "discord_notifier",
    "snyk-run", #Type of message to send for above discord notifier
]

merge_steps = [
    "clone_repository",
    "python_version",
    "execute_scripts",
    "discord_notifier",
    "python-script", #Type of message to send for above discord notifier
    "sonarqube_trigger",
    "discord_notifier",
    "sonarqube-run", #Type of message to send for above discord notifier
    "snyk_analysis",
    "discord_notifier",
    "snyk-run", #Type of message to send for above discord notifier
    # TODO: Integration Tests ...
]

pr_nightly_steps = [
    "clone_repository",
    "python_version",
    "execute_scripts",
    "discord_notifier",
    "python-script", #Type of message to send for above discord notifier
    "sonarqube_trigger",
    "discord_notifier",
    "sonarqube-run", #Type of message to send for above discord notifier
    "snyk_analysis",
    "discord_notifier",
    "snyk-run", #Type of message to send for above discord notifier
]
