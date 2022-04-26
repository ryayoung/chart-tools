from chart_tools.data.source import source


class DataSource(Source):
    """
    Here's the documentation
    """

    def __init__(self, user=None, repo=None, branch=None, path="", name=None):

        if user and repo and branch:
            super().__init__(user, repo, branch, path)
            if name:
                self.name = name
            else:
                self.name = self.repo
            return

        elif name and "default_lib" in globals():
            if default_lib.sources == None:
                raise ValueError("There are no predefined sources to choose from")
            # Create a DataSource by using only the name of a pre-defined one
            source = default_lib.sources.get(name, None)
            if not source:
                raise ValueError(f"Unknown source, '{name}'")

            super().__init__(source.user, source.repo, source.branch, source.path)
            self.name = name
            return

        else:
            self.user = user if user else ""
            self.repo = repo if repo else ""
            self.branch = branch if branch else ""
            self.path = path if path else ""
            self.name = name
    

    def __repr__(self):
        if self.name != None:
            return f"{self.name}:{(10-len(self.name))*' '}{self.root}"
        else:
            return f"{self.user}/{self.repo}:{(20-(len(self.repo)+len(self.repo)))*' '}{self.root}"


    def display_datasets(self, header=True, trunc=1000):
        if self.datasets == []:
            return
        if header:
            if self.name != None:
                print(f"Datasets for '{self.name}':")
            if self.name == None:
                print(f"Datasets in '{self.user}/{self.repo}/{self.path}':")
            if len(self.subdirs) > 0:
                print("(refer files inside folders using the full path. Ex: 'folder/file')")
            print("---------------------------")
        
        # Files in base directory
        for file in [f for f in self.datasets if "/" not in f]:
            print(f"  {file}")

        # Files in subdirectories
        count = 0
        for dir in self.subdirs:
            print(f"  {dir}/")
            count += 1
            for f in self.dir_contents(dir):
                count += 1
                if count > trunc: break
                print(f"    {f}")

            if count > trunc: break

        if count > trunc:
            name = self.name if self.name else f"{self.user}/{self.repo}"
            print(f"      ({len(self.datasets)-count} more files in {name})")
    

    def display_subdirs(self):
        print(f"Sub-directories in '{self.user}/{self.repo}/{self.path}'")
        print("---------------------------------------")
        print("  ", end="")
        print(*self.subdirs, sep="\n  ")
