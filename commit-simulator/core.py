from query_commits import query_commits
from markov_chain import MarkovChain

ILLEGAL_CHARS = '#!.,:*%&\/()[]{}$?^0123456789'

class CommitSimulator:

    def __init__(self, commits):
        self.commits = commits
        self._chain = MarkovChain()


    def train_markov_chain(self):
        chain = MarkovChain()
        commit_words = self._split_messages(self.commits)
        for commit in commit_words:
            self._chain.populate_chain(commit)


    def get_markov_string(self):
        result = self._chain.choose_path()
        return " ".join(result)

    def _split_messages(self, commits):
        """ split commit messages to words """
        commit_words = [] # list of lists of words
        for msg in commits:
            words = []
            for word in msg.split():
                if not any(c in ILLEGAL_CHARS for c in word):
                    words.append(word.lower())
            if not len(words) == 0:
                commit_words.append(words)
        return commit_words



if __name__ == "__main__":
    commits = query_commits()
    cs = CommitSimulator(commits)
    cs.train_markov_chain()
    for x in range(20):
        print(cs.get_markov_string())
    # print(cs._chain.print_states())
    print("States count: {0}".format(len(cs._chain._states)))
