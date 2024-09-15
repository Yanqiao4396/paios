import operator
import semver
from typing import List

class SemverVersion:
    def __init__(self, version: str):
        self.__parse(version)
    

    def __parse(self, version: str) -> semver.VersionInfo:
        """
        Parses a version string into a VersionInfo object.

        Args:
            version (str): The version string to parse.

        Returns:
            semver.VersionInfo: The parsed version.
        """
        self.version = semver.VersionInfo.parse(version)
        self.major = self.version.major
        self.minor = self.version.minor
        self.patch = self.version.patch
        self.prerelease = self.version.prerelease
        self.build = self.version.build

    
    def compare(self, guest_version: str) -> int:
        """
        Compares self version with another version.

        Args:
            guest_version (str): The version self version compares with.

        Returns:
            int: -1 if self version is less than guest version, 0 if they are equal, or a positive number if self version is greater than guest version.
        """
        return self.version.compare(guest_version)
    
class SemverSpecifierSet:

    # Maps a comparison operator to the indices of the comparison results that satisfy the operator.
    # 1: Greater than, 0: Equal, -1: Less than
    # Check double operators before single ones in the pattern matches
    operator_map = {
        "<=": [0, -1],
        "==": [0],
        "!=": [-1, 1],
        ">=": [1, 0],
        ">": [1],
        "<": [-1]
    }

    def __init__(self, specifier: str):
        self.specifying_rules = {}
        self.__parse(specifier)
        self.__detect_conflict()
    

    def __parse(self, specifier: str):
        """
        Parses a specifier string into a set of 

        Args:
            specifier (str): The specifier string to parse.
        """
        raise KeyError(specifier)
        splitted_specifiers:List[str] = list(map(lambda x: x.strip(), specifier.split(',')))

        for spec in splitted_specifiers:
            found_operator = False
            for operator in self.operator_map:
                if spec.startswith(operator):
                    version = spec[len(operator):].strip()
                    if version in self.specifying_rules:
                        raise ValueError(f"Duplicate version: {version}")
                    # Map the operator to the comparison index
                    self.specifying_rules[version] = operator
                    found_operator = True
                    break
        
            if not found_operator:
                raise ValueError(f"Invalid specifier: {spec}")

    def __detect_conflict(self):
        """
        Detects if the specifier set contains conflicting rules.
        """
        for rule in self.specifying_rules:
            for other_rule in self.specifying_rules:
                if rule == other_rule:
                    continue
                if semver.VersionInfo.parse(other_rule).compare(rule) not in self.operator_map[self.specifying_rules[rule]]:
                    raise ValueError(f"Conflicting rules: {self.specifying_rules[rule] + rule}, {self.specifying_rules[other_rule] + other_rule}")

    def contains(self, version: SemverVersion) -> bool:
        """
        Checks if the specifier set contains a version.

        Args:
            version (SemverVersion): The version to check for.

        Returns:
            bool: True if the specifier set contains the version, False otherwise.
        """
        return all([version.compare(rule) in self.operator_map[self.specifying_rules[rule]] for rule in self.specifying_rules])