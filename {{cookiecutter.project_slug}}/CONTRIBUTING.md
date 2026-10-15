## Commit Guidelines

We have very precise rules over how our git commit messages can be formatted. This leads to more readable messages that are easy to follow when looking through the project history.

### General Rules

1.  Separate subject from body with a blank line
2.  Limit the entire header, including type and scope, to 70 characters
3.  Keep the type lowercase; capitalize the first word of the subject
4.  Do not end the subject line with a period
5.  Use the imperative mood in the subject line
6.  Use the body to explain what and why vs. how
7.  Each commit should be a single, stable change

### Commit Message Format

Each commit message consists of a mandatory **header**, an optional **body**,
and an optional **footer**. Include a body unless the header explains the
entire change, such as a typo fix.

The header has a special format that includes a type and a subject:

```
<type>[(<scope>)]: <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The scope is optional and names the affected component. Omit it when no
clear, established scope applies. Square brackets in the template indicate
optional content; do not include them in the actual message.

Limit the entire header to 70 characters. Wrap body and footer prose at
72 characters, with a hard maximum of 100 characters per line.

Put known Jira or GitHub issue references in the footer. Use `Fixes` or
`Closes` only when the change resolves the issue; otherwise use `Refs`.
For Sentry issues, use `Sentry: <issue URL>`. Omit unknown references and
omit the footer when there are no references or breaking changes.

For example, a short change:

```
fix: Handle special characters in video filename

S3 rejects filenames with unicode characters, so uploads of such videos
failed.

Strip those characters from the filename before uploading.

Fixes DJANGO-1234
```

And a larger change, with a list and a note on verification:

```
build: Upgrade Python dependencies to fix Dependabot alerts

Bump packages with open security advisories, other than Django, which
needs its own 4.0 -> 4.2 LTS upgrade.

Pinned in pyproject.toml:
- gunicorn 20.1.0 -> 22.0.0
- requests 2.28.2 -> 2.34.2
- sentry-sdk 1.11.1 -> 1.45.1

Transitive, refreshed in uv.lock: urllib3, cryptography, sqlparse.

The full suite passes locally (2366 tests). gunicorn is production-only,
so the tests do not exercise it.
```

#### Revert

If the commit reverts a previous commit, it should begin with `revert:`, followed by the header of the reverted commit. In the body it should say: `This reverts commit <hash>.`, where the hash is the SHA of the commit being reverted.

#### Type

Must be one of the following:

| Type | Use for |
| --- | --- |
| `build` | Build system or external dependency changes |
| `ci` | CI configuration files and scripts |
| `docs` | Documentation only changes |
| `feat` | A new feature |
| `fix` | A bug fix |
| `perf` | A code change that improves performance |
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `style` | Formatting changes that do not affect code behavior |
| `test` | Adding or correcting tests |
| `meta` | Repository tooling, such as pre-commit hooks or editor config |
| `license` | License changes |
| `revert` | Reverting a previous commit |


#### Subject

The subject contains a succinct description of the change:

- Use the imperative, present tense: “change” not “changed” nor “changes”
- Capitalize the first letter
- No dot (.) at the end

#### Body

Use natural prose in the body; imperative mood is required only in the
subject. Include the motivation for the change and explain previous behavior
when relevant.

Write the body so a person can skim it, not as one block of text:

- Wrap lines at 72 characters. Never leave a paragraph as a single long line.
- Keep each paragraph to one idea, 1–3 sentences, with a blank line between paragraphs.
- Start with the problem: what was wrong or missing, and who it affected.
- Then say what the commit changes and why that fixes it. Leave out how the code works unless it is not obvious from the diff.
- Use a `-` list when you have three or more parallel items (files, packages, versions, tests). Put each item on its own line.
- End with how you verified it, if that is not obvious (for example, “The full suite passes locally”). Mention anything you did not verify.
- Skip the body only when the subject says everything, such as a typo fix.

#### Footer

The footer should contain any information about **Breaking Changes** and is also the place to reference GitHub issues that this commit **Closes**.

Describe breaking changes in a footer beginning with `BREAKING CHANGE: `,
followed by the impact and any migration steps. Wrap continuation lines
using the same limits as the body.

### Instructions for AI-generated commit messages

- Read the staged diff and relevant user context before drafting a message.
- Describe the resulting change, not the steps taken during implementation.
- Do not invent issue IDs, motivations, test results, or verification claims.
- Include verification only when there is evidence it was performed.
- Mention relevant verification gaps; do not imply unrun tests passed.
- Check the allowed type, capitalization, imperative subject, line lengths,
  and blank lines before returning the message.
- When asked only for a commit message, return the message without commentary
  or Markdown fences.

References

- [https://chris.beams.io/posts/git-commit/](https://chris.beams.io/posts/git-commit/)
- [https://conventionalcommits.org/](https://conventionalcommits.org/)
- [https://github.com/angular/angular/blob/master/CONTRIBUTING.md](https://github.com/angular/angular/blob/master/CONTRIBUTING.md)

## **Code Reviews are for …**

**Identifying problematic code**

Above all, a code review should try to identify potential bugs that could cause the application to break – either now, or in the future.

- Uncaught runtime exceptions (e.g. potential for an index to be out of bounds)
- Obvious performance bottlenecks (e.g. `O(n^2)` where `n` is unbounded)
- Code alters behavior elsewhere in an unanticipated way
- API changes are not backwards compatible (e.g. renaming or removing a key)
- Complex ORM interactions that may have unexpected query generation/performance
- Security vulnerabilities
- Tests do not verify the implemented behavior

**Assessing and approving long-term impact**

If you’re making significant architectural, schema, or build changes that will have long-term ramifications to the software or data, it is necessary to solicit a senior engineer’s acknowledgment and blessing.

- Large refactors
- Database schema changes, like adding or removing columns and tables
- API changes (including JSON schema changes)
- Adopting new frameworks, libraries, or tools
- New product behavior that may permanently alter performance characteristics moving forward

**Double-checking expected behavior**

The reviewer should make a genuine attempt to double-check that the goals of the PR appear to be satisfied by the code submitted. This requires the submitter to write a good description of the expected behavior, and why. *See also: Guidelines for submitters* *below*.

**Information sharing and professional development**

Code reviews are an opportunity for more people to understand forthcoming code changes, so that they might in turn teach others down the road, and be in a position to fix something if/when the original author is not be available.

Additionally, code reviews are an opportunity to learn about new techniques or approaches, and be exposed to code you might otherwise not have an opportunity to browse.

**Reducing code complexity**

Research shows that LOC is correlated with a higher bug count. If reviewers see an easy opportunity to significantly reduce the amount of code that is submitted, they should suggest a different approach.

For example, if a submitter has written a `for` loop to find an item in an array:

```
for (let i = 0; i < arr.length; i++) {
  if (arr[i] === 'thingiwant') return i;
}
return undefined;
```

It’s fair game to suggest they instead use:

```
const index = arr.indexOf('thingiwant');
return index === -1 ? undefined : index;
```

This is a mostly objective improvement: there are fewer variables, fewer statements, and fewer branches, and the method name `indexOf` communicates intent. Suggesting these types of uncontroversial improvements are encouraged.

Be careful though – it’s easy to go down a rabbit hole of re-writing code to be as small as possible, and in the end winding up with something ultimately more complicated. Be pragmatic and strive to reach a good balance. *See also: “Code reviews are not for getting it perfect” below.*

**Enforcing coding standards**

As much as possible, we use automation to enforce code style, code coverage, and other industry-accepted good practices. But there are exceptions that cannot necessarily automated (or perhaps more accurately, we haven’t automated *yet*):

- Variable, file, and metric names are consistent with existing code
- Migrations have a deployment plan
- Unused or superfluous code isn’t committed accidentally

## **Code Reviews are not for …**

**Passing responsibility onto the reviewer**

It is not the responsibility of the reviewer that your code is correct, is bug free, or achieves its goals. Reviewers are there to help you, but if something is wrong, it’s your responsibility to correct it.

**Boasting about your programming knowledge**

As a reviewer, try to stick to objective improvements and make a best-intent assumption that the submitter has done their homework. Sentry is a No Flex Zone™.

**Introducing long-term architectural changes for the first time**

While code reviews are great for discussion, they’re not the place to introduce large, long-term changes for the first time. Before dropping a PR that implements those changes, you should write a proposal and reach out to the relevant parties beforehand.

**Getting it perfect**

Code reviews are expensive. Every time you request a change, you’re probably delaying that PR by 24 hours or more. This can severely inhibit our ability to move fast.

The goal of code reviews is to **reduce risk**, not to produce perfect code. It’s okay to ship code in stages, and to commit to improving something later. If you’re thinking – *if we don’t get it correct up-front, we’*ll *never come back to it* – consider that if it never needs coming back to, perhaps those changes were never necessary in the first place.

> Perfect is the enemy of the good. – Voltaire, probably

Please be pragmatic, and consider the cost of each incremental request for changes.

## Guidelines for *Submitters*

**Try to organize your work in a way that makes it conducive to review**

- Ideally, a pull request is limited to only a single feature or behavior change.
- This might feel like more work up-front, but it can make code review faster, reduce risk by letting you ship in stages, and ultimately end up being quicker.

**Describe what your PR does in a few sentences in the description field**

- Additionally explain **_why_** we’re making these changes.
- If applicable, explain why other approaches were explored but not settled on.
- This gives the reviewer context, and prevents them going down the same rabbit holes that that submitter may have already explored when creating the code.

**Where appropriate, label in-progress PRs as WIP (work in progress) for early feedback**

- Labeling your work as WIP helps set expectations about the state of the PR.
- WIP PRs are good for having someone check-in to make sure you’re on the right path.
- Additionally, this is an opportunity to verify CI passes before involving a reviewer.

**Be your own first reviewer**

- After you’ve put up your PR on GitHub, walk through the code yourself, before assigning an external reviewer.
- You’ll often catch code mistakes you didn’t see when writing it.
- This is also a good time to leave comments and refresh your memory in order to write a more helpful description.

**Avoid rebasing unnecessarily**

- After a rebase, previous review comments will be orphaned from their now non-existent parent commits, making review more difficult
- Rewriting history makes it difficult for reviewers to isolate the scope of their review

**Let reviewers know that you’ve made changes**

- Request review again via basecamp.
- Don’t rely on reviewers mind-reading skills to know that you’re ready to have them look things over again.
- If you resolve a point of actionable feedback, it's helpful to leave a comment to let the reviewer know that it was addressed, ideally with a reference to the commit that addressed it.

## Guidelines for *Reviewers*

**Be polite and empathetic**

- Avoid accusatory and/or judgmental comments like: “You should have done X”

**Provide** **_actionable_** **feedback**

- Instead of *“This is bad”*, try *“I feel this could be clearer. What if you renamed variable X to Y?”*

**Distinguish between “requires changes” and “nitpicks”**

- Consider marking a PR as approved if the only requested changes are minor nits, so as not to block the author in another asynchronous review cycle.

**Respond promptly to code review requests**

- We’re a team – *[we ride together, we die together](https://www.youtube.com/watch?v=1d5Q0vXbODs)* – and you need to unblock other developers so that we can all move forward.
- We recommend checking for open code reviews at the start and end of every day.
- [Github's Review Requests tab](https://github.com/pulls/review-requested) can be a helpful place to keep track of these.


References

- [https://develop.sentry.dev/code-review/](https://develop.sentry.dev/code-review)
