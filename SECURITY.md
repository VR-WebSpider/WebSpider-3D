<!-- SPDX-FileCopyrightText: 2026 WebSpider Studios -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Security Policy

## Reporting A Vulnerability

Report security issues privately to:

- Rahul `<rahul@webspider3d.com>`

Do not open a public GitHub issue for vulnerabilities, secrets, credential leaks, exploit details, or private user data.

Include:

- A concise description of the issue
- Affected version, commit, or release artifact
- Reproduction steps, if safe to share privately
- Impact and any known workaround

Do not include real WebSpider 3D account passwords, API keys, production tokens, private scene data, or third-party secrets in reports.

## Scope

In scope:

- WebSpider 3D Blender-side client code in this repository
- Build, packaging, update, and source-distribution behavior for this client
- Client-side handling of tokens, local credentials, user files, and network requests

Out of scope for this public repository:

- WebSpider 3D hosted backend service source code
- WebSpider 3D production infrastructure
- Third-party platform vulnerabilities unless they directly affect the WebSpider 3D client

## Supported Versions

The current public source release is the supported security review target.

For release source mapping, see [SOURCE_CORRESPONDENCE.md](SOURCE_CORRESPONDENCE.md).
