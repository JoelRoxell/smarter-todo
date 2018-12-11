class Issue():
    title_size = 40

    def __init__(self, title, labels, estimate):
        self.title = title
        self.labels = labels
        self.estimate = estimate

    def to_github_issue(self):
        return {
            'title': self.title[:self.title_size] + ('...' if len(self.title) > self.title_size else '') + ' ({})'.format(self.estimate),
            'body': self.title,
            'labels': self.labels
            # "assignees": [],
        }
