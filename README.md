# Smart Mobile Robots - Robo Monitor IoT

Develop a monitoring system that records temperature and
humidity by saving them to a CSV file. In case of disconnection from the Wi-Fi network, the
data is recorded locally and, when the connection is reestablished, it is
sent to a MongoDB database via an API developed in Python.
The application must also allow data queries via requests using
Swagger.

If you want to know more about the specifications of this project, read the job [requirements doc](./docs/requirements-doc.pdf).

## Tech Stack

<!--- # "Verify icons availability here https://github.com/tandpfun/skill-icons" -->

[![My Skills](https://skillicons.dev/icons?i=python,mongodb)](https://skillicons.dev)

## Getting Started

Add the following to gettin's started

1. **Clone project**:

```bash
git clone https://github.com/MatheusHenrique129/robo-monitor-iot.git
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Running the project**:

In the root path, run the command:

```bash
fastapi dev main.py
```

## 📫 Contribute

Here you will explain how other developers can contribute to your project. For example, explaining how can create their branches, which patterns to follow and how to open an pull request

1. Clone project

```bash
git clone https://github.com/MatheusHenrique129/robo-monitor-iot.git
```

2. Create feature/branch:

```bash
  git checkout -b feature/NAME
```

3. Follow [commit patterns](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716).

4. Open a [Pull Request](https://www.atlassian.com/br/git/tutorials/making-a-pull-request) explaining the problem solved or feature made, if exists, append screenshot of visual modifications and wait for the review!

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MatheusHenrique129"><img src="https://avatars.githubusercontent.com/u/67923259?v=4?s=100" width="100px;" alt="Matheus Henrique"/><br /><sub><b>Matheus Henrique</b></sub></a><br /><a href="#maintenance-MatheusHenrique129" title="Maintenance">🚧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

### License

This software is available under the following licenses: [MIT](https://rem.mit-license.org)
