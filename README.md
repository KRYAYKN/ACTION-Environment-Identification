# **Overview**

This action is designed to provide an easy and centralized way to dynamically pointing a pipeline to an repository environment.
Based on multiple possible criterias a pipeline can decide to which environments that execution will pointing to.
Allow us to reuse the same pipeline for multiple environments.

### Dependencies:
Python: 3.10

### Inputs:

> Unfortunatelly at the moment, composite actions has a problem to properly evaluate boolean type parameters. Composite actions only allow, for now, string parameters.
Pay attention to always informing these parameters lowercase.
For more info: https://github.com/actions/runner/issues/2238

| **source-branch** <img width=78/> | <img width=575 />                                                       |
| ---                         | ---                                                                           |
| Description                 | The source branch this action will use to calculate the environment           |
| Type                        | String                                                                        |
| Default                     |                                                                               |
| Required                    | Yes                                                                           |
| Example                     | `source-branch: feature/jira-123`                                             |

| **destination-branch** <img width=43/> | <img width=575 />                                                  |
| ---                         | ---                                                                           |
| Description                 | The destination branch this action will use to calculate the environment      |
| Type                        | String                                                                        |
| Default                     |                                                                               |
| Required                    | Yes                                                                           |
| Example                     | `destination-branch: qa`                                                      |

| **event-name** <img width=95/> | <img width=575 />                                                          |
| ---                         | ---                                                                           |
| Description                 | The type of event that trigger the pipeline                                   |
| Type                        | String                                                                        |
| Default                     |                                                                               |
| Required                    | Yes                                                                           |
| Example                     | `event-name: ${{ github.event_name }}`                                        |

| **list-ignore-validation-for-environments** <img width=95/> | <img width=575 />                                                              |
| ---                         | ---                                                                                                            |
| Description                 | List of all environment with information if we should ignore the validation for that environment               |
| Type                        | String ( JSON )                                                                                                |
| Default                     | `{}`                                                                                                           |
| Required                    | No                                                                                                             |
| Example                     | `list-ignore-validation-for-environments: '{ "PROD": false, "PREPROD": false, "QA": false, "STAGING": false '` |

### Outputs:

| **validation-environment** <img width=10/> | <img width=575 />                                              |
| ---                         | ---                                                                           |
| Description                 | The validation environment that the pipeline should use                       |
| Type                        | String                                                                        |
| Possible values             | `"QA-VALIDATION","STAGING-VALIDATION","PREPROD-VALIDATION","PROD-VALIDATION"` |

| **release-environment** <img width=30/> | <img width=575 />                                                 |
| ---                         | ---                                                                           |
| Description                 | The release environment that the pipeline should use                          |
| Type                        | String                                                                        |
| Possible values             | `"QA-RELEASE","STAGING-RELEASE","PREPROD-RELEASE","PROD-RELEASE"`             |

| **ignore-validation-for-environment** <img width=30/> | <img width=575 />                                   |
| ---                         | ---                                                                           |
| Description                 | Information if we should ignore the validation for the current environment    |
| Type                        | String                                                                        |
| Possible values             | `"true","false"`                                                              |

### Available Versions:
