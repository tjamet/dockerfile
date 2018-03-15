# dockerfile [![Build Status](https://travis-ci.org/dependencies-io/dockerfile.svg?branch=master)](https://travis-ci.org/dependencies-io/dockerfile)

A [dependencies.io](https://www.dependencies.io) component that updates base images of Dockerfiles.

## Usage

```yml
version: 2
dependencies:
- type: dockerfile
  path: app/Dockerfile
```

There are also [additional settings available](https://github.com/dependencies-io/deps#dependenciesyml) for
further customizing how updates are made.

## Support

Any questions or issues with this specific actor should be discussed in [GitHub
issues](https://github.com/dependencies-io/dockerfile/issues). If there is
private information which needs to be shared then you can instead use the
private support channels in dependencies.io.
