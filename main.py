#!/bin/env python3

from dataclasses import dataclass
from enum import Enum
from os import getenv

from functions import set_gha_output

destination_branch = getenv("BRANCH_DESTINATION").lower()
source_branch = getenv("BRANCH_SOURCE").lower()
event = getenv("EVENT_NAME")

class ExtendedEnum(Enum):
    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())


class RepositorySpecialPrefixes(str, ExtendedEnum):
    VALIDATION = "validation/"
    RELEASE = "release/"
    DEPLOY = "deploy/"
    HOTFIX_FEATURE = "hotfix/"
    HOTFIX = "release/hotfix-"
    BUGFIX = "fix/"
    FEATURE = "feature/"
    FEAT = "feat/"
    RETRIEVE = "pulldown/"
    HELPER = "helper/"
    WRONG_FEATURE_FORMAT_ONE = "feature-"
    WRONG_FEATURE_FORMAT_TWO = "feat-"


class OldConventionBranchNames(str, ExtendedEnum):
    STAGING = "DEVELOP"
    PROD = "MASTER"


class AvailableReleaseTypes(str, ExtendedEnum):
    REGULAR = "RELEASE"
    HOTFIX = "HOTFIX"
    BUGFIX = "BUGFIX"
    VALIDATION_ONLY = "VALIDATION_ONLY"
    FORCE_DEPLOY = "FORCE_DEPLOY"
    INVALID = "INVALID"
    HELPER = "HELPER"
    RETRIEVE = "RETRIEVE"


class AvailableEnvironments(str, ExtendedEnum):
    QA = "qa"
    PREPROD = "preprod"
    PROD = "prod"
    INVALID = "invalid"


class AvailableReleaseEnvironments(str, ExtendedEnum):
    QA = "QA-RELEASE"
    PREPROD = "PREPROD-RELEASE"
    PROD = "PROD-RELEASE"
    INVALID = "INVALID"


class AvailableValidationEnvironments(str, ExtendedEnum):
    QA = "QA-VALIDATION"
    PREPROD = "PREPROD-VALIDATION"
    PROD = "PROD-VALIDATION"
    INVALID = "INVALID"


@dataclass
class EnvironmentInformation:
    source: str
    target: str
    releaseType: AvailableReleaseTypes
    releaseEnvironment: AvailableReleaseEnvironments
    validationEnvironment: AvailableValidationEnvironments

    def __str__(self) -> str:
        return f"""
Processing Result...

Branch Information:
Source: {self.source}
Destination: {self.target}

Choosed environments:
Type: {self.releaseType.upper()}
Release: {self.releaseEnvironment}
Validation: {self.validationEnvironment}
        """


def raise_error(source, destination, message) -> None:
    raise ValueError(message, source, destination)


def set_github_actions_variables(
    environment: EnvironmentInformation, branch: AvailableEnvironments
) -> None:
    set_gha_output("release-environment", environment.releaseEnvironment)
    set_gha_output("validation-environment", environment.validationEnvironment)
    set_gha_output("release-type", environment.releaseType)
    set_gha_output("environment", branch.upper())


print("Input Values:")
print(f"{source_branch=}")
print(f"{destination_branch=}")

if destination_branch.upper() in OldConventionBranchNames.values():
    destination_branch = OldConventionBranchNames(destination_branch.upper()).name
    print("")
    print("Old convention name detected!")
    print(f"New destination branch: {destination_branch}")

if source_branch.upper() in OldConventionBranchNames.values():
    source_branch = OldConventionBranchNames(destination_branch.upper()).name
    print("")
    print("Old convention name detected!")
    print(f"New source branch: {source_branch}")

branch = destination_branch
environmentInfo = None
release_type = AvailableReleaseTypes.INVALID
release_environment = None
validation_environment = None

if source_branch.startswith(RepositorySpecialPrefixes.FEATURE) and destination_branch == AvailableEnvironments.QA:
    branch = AvailableEnvironments.QA
    release_type = AvailableReleaseTypes.REGULAR
elif source_branch == "promotion/qa" and destination_branch == "qa":
    release_env = "QA-RELEASE"
    validation_env = "QA-VALIDATION"
elif destination_branch.startswith(RepositorySpecialPrefixes.RELEASE) and source_branch == AvailableEnvironments.QA:
    branch = AvailableEnvironments.PREPROD
    release_type = AvailableReleaseTypes.REGULAR

elif source_branch.startswith(RepositorySpecialPrefixes.BUGFIX) and destination_branch != AvailableEnvironments.PROD:
    branch = destination_branch
    release_type = AvailableReleaseTypes.BUGFIX

elif source_branch.startswith(RepositorySpecialPrefixes.HOTFIX):
    branch = destination_branch
    release_type = AvailableReleaseTypes.HOTFIX

elif destination_branch == AvailableEnvironments.PROD and source_branch.startswith(RepositorySpecialPrefixes.RELEASE):
    branch = AvailableEnvironments.PROD
    release_type = AvailableReleaseTypes.REGULAR


if not release_type == AvailableReleaseTypes.INVALID:
    if release_environment is None:
        release_environment = AvailableReleaseEnvironments[branch.upper().replace('-', '')].value
    if validation_environment is None:
        validation_environment = AvailableValidationEnvironments[branch.upper().replace('-', '')].value
else:
    release_environment = AvailableReleaseEnvironments.INVALID
    validation_environment = AvailableValidationEnvironments.INVALID

environmentInfo = EnvironmentInformation(
    source=source_branch,
    target=destination_branch,
    releaseType=release_type,
    releaseEnvironment=release_environment,
    validationEnvironment=validation_environment,
)

set_github_actions_variables(environmentInfo, branch)

print(environmentInfo)

if (
    environmentInfo.releaseEnvironment == AvailableReleaseEnvironments.INVALID
    and environmentInfo.validationEnvironment == AvailableValidationEnvironments.INVALID
):
    raise_error("Invalid information provided", source_branch, destination_branch)



