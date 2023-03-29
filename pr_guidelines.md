## Work in progress #311216


The following are recommendations for your Pull Request and the "lifecycle" of your branch. As always there are flexibilities, but we should strive to follow these as close as we can.
## Keep your PR atomic
Keeping your PR atomic means that you should try to limit the scope of the changes you are proposing in a single PR. Here are some reasons why this is important:

- Easier to review: An atomic PR is easier to review since it has a well-defined scope and can be understood and tested quickly.

- Faster feedback loop: With an atomic PR, reviewers can provide feedback faster, and developers can respond to that feedback quickly.

- Easier to merge: An atomic PR is easier to merge because it reduces the likelihood of merge conflicts, and it is easier to ensure that the code is compatible with the rest of the project.

- Better for collaboration: An atomic PR encourages collaboration since developers can work on smaller parts of the codebase independently, without worrying about how their changes will affect the rest of the project.

- Better for testing: An atomic PR allows for better testing since the changes are smaller and more focused. This makes it easier to identify and fix bugs and reduces the likelihood of introducing new ones.

Overall, keeping your PR atomic helps to improve the quality and efficiency of the development process, making it easier for everyone involved to work together towards a common goal.

# Link your commits to tasks.

To link your commits to tasks in Azure DevOps, you can use the syntax `#<task-id>` in your commit message. Here's an example:

```
git commit -m "Feat: Implemented feature X. #1234"
```

In this example, 1234 is the ID of the task in Azure DevOps. Once you push your changes to the remote repository, Azure DevOps will automatically detect the task ID in the commit message and link it to the corresponding task.

By linking your commits to tasks in Azure DevOps, you can keep track of the progress of your tasks and easily trace the changes made to the codebase back to the tasks they were associated with.

# Keep your commit messages relevant.

When creating a commit message, it's important to think about the purpose of the commit and how it fits into the overall development of the project. Here are some tips to keep in mind:

- Keep it concise: The commit message should be concise and to the point. A good rule of thumb is to keep it under 50 characters.

- Use the imperative mood: The commit message should start with an imperative verb (e.g., "Add", "Update", "Fix") that describes the action taken in the commit.

- Be specific: The commit message should be specific about what was changed and why it was changed. It should not be vague or general.

- Include references: If the commit is related to a task or issue, include a reference to it in the commit message (e.g., "Fix issue #1234").

- Consider the audience: Remember that the commit message is not just for yourself, but also for your team and future developers who may need to understand the changes made. Make sure the message is clear and understandable for everyone.

- Keep it tidy: Make sure the commit message is tidy, with proper punctuation and formatting. Avoid excessive capitalization or unnecessary words.

In the following example of a commit message, we are fixing a bug:

```
git commit -m "Fix: Mlflow error message when logging LightGBM model. #10001"
```

# Branching Workflow

## 1. Creating your **Feature** branch
Normally you will be assigned a Story to work in a **Feature**, this feature will become a branch and this branch will be based on the **Release** branch.

## 2. Add commits to your **Feature** branch
Once you have your branch checked out you can start to add commits to it, following the previously mentioned guidelines.

## 3. When ready to merge, Pull changes back from the **Release** branch (update)
Once your code is completed you need to pull back or merge back from the **Release** branch to update your branch with possible changes that might have happened in the **Release** branch, this will save you some headaches before you try to merge back to **Release** because you can resolve the conflicts (if any) in your own branch.

## 4. Create a Pull Request(PR) to the **Release** branch
In Azure DevOps create a Pull Request, fill out the Checklist, invite your teammates, and this will in place trigger a code review.

## 5. Complete the Pull Request
When you have resolved the PR feedback and the PR is accepted, complete your pull request.

Use Merge type Merge and Delete your feature branch after merging.

![image.png](/.attachments/image-7889d3d4-8ca1-4f36-b6a7-f1573fdaecc9.png)

### The following diagram is an example of how our git branching workflow works

In here we can see that we:
- Created the **nice_feature** branch based on **Release**.
- Committed a few changes to it
- Updated back from **release** branch (merged)
- Finally created a PR back into **Release**.

From there on is a back and forth process between you and Team Eagle in where we might have to fix something that we didn't catch in the code review process.

Once is merged into Release it will trigger a Continuous Integration pipeline that will release your code to the **DEV** and **UAT** environment in where it will be tested.

Team Eagle will work with you and the stakeholders to decide when this feature will need to be merged into Main and that successful merge will trigger the automatic deployment into our **PRODUCTION** environment.


::: mermaid
gitGraph
    commit id: " "
    commit id: "Stable Prod" tag: "v1.0.0"
    branch release
    commit id: "Stable Release 1"
    commit id: "Stable release 2"
    branch nice_feature
    checkout nice_feature
    commit id: "Feat: Added a thing. #1234"
    checkout release
    commit id: "Feat: Different feature. #1236"
    checkout nice_feature
    commit id: "Fix: Error when adding thing. #1235"
    commit id: "Feat: Final touches to the nice_feature. #1237"
    merge release id: "Merge: Update this branch from release" type: HIGHLIGHT
    checkout release
    merge nice_feature id: "PR: Update release with the nice_feature" tag: "RCv2.0.0"
    commit id: "PR: feedback" tag: "RCv2.0.1"
    checkout main
    merge release id: "PR: Add nice_feature to Prod" tag: "v2.0.1"
    commit id: "Fix: Hotfix about the nice_feature" tag: "v2.0.2"
    checkout release
    merge main id: "Update release with main's changes"
    branch very_nice_feature
    checkout very_nice_feature
    commit id: "Feat: Add a very nice feature. #1238"
    commit id: "Feat: Another part of the very nice feature. #1239"
    commit id: "Fix: Errors in the very nice feature. #1240"
    merge release id: "Merge: Update this branch from release again" type: HIGHLIGHT
    checkout release
    merge very_nice_feature id:"PR: Update release with the very_nice_feature"tag:"RCv2.1.0"
    checkout main
    merge release id:"PR: Add the very_nice_feature to Prod" tag:"v2.1.0"

:::

After this you can see how in the diagram, we have another Story about creating a very nice feature and we have to branch again from **Release**, but now **Release** have all the changes up to that point, so we follow the same process again in our **very_nice_feature** branch.

## A few things to know
- **Main** branch (or master) is Production, and we have CI/CD pipelines that will trigger on merge.
- **Release** branch is Dev and UAT (or Test)
- Only Team Eagle pushes to **Main**
- Everyone else can create a Pull Request (PR) to **Release**
- Before merging your **Feature** branch to **Release** always update from Release first (merge from)
- Always delete your **Feature** branch after a successful merge to **Release**
- Don't Auto-Complete your PR
- Try to resolve all the feedback before completing the PR