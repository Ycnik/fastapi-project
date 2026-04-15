# syntax=docker.io/docker/dockerfile-upstream:1.22.0
# check=error=true

ARG PYTHON_MAIN_VERSION=3.14
ARG PYTHON_VERSION=${PYTHON_MAIN_VERSION}.3
ARG UV_VERSION=0.11.0

# ------------------------------------------------------------------------------
# S t a g e   b u i l d e r
# ------------------------------------------------------------------------------
# dhi.io/uv:0.10.10-debian13
FROM ghcr.io/astral-sh/uv:${UV_VERSION}-python${PYTHON_MAIN_VERSION}-dhi AS builder

WORKDIR /opt/app

# Enable bytecode compilation
# Copy from the cache instead of linking since it's a mounted volume
# Kein Python-Download erforderlich
# https://github.com/astral-sh/uv/issues/8635#issuecomment-2759670742
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_NO_MANAGED_PYTHON=true \
    UV_SYSTEM_PYTHON=true

# .venv erstellen
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    ["/usr/local/bin/uv", "venv"]
# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    ["/usr/local/bin/uv", "sync", "--frozen", "--no-install-project", "--no-default-groups", "--no-editable"]

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY LICENSE README.md pyproject.toml ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    ["/usr/local/bin/uv", "sync", "--frozen", "--no-default-groups", "--no-editable"]

# ------------------------------------------------------------------------------
# S t a g e   f i n a l
# ------------------------------------------------------------------------------
FROM dhi.io/python:${PYTHON_VERSION}-debian13 AS final

# Anzeige bei "docker inspect ..."
# https://specs.opencontainers.org/image-spec/annotations
# https://spdx.org/licenses
# MAINTAINER ist deprecated https://docs.docker.com/engine/reference/builder/#maintainer-deprecated
LABEL org.opencontainers.image.title="soldat" \
    org.opencontainers.image.description="Appserver soldat mit Basis-Image Bookworm" \
    org.opencontainers.image.version="2026.4.1-bookworm" \
    org.opencontainers.image.licenses="GPL-3.0-or-later"
    
# "working directory" fuer die Docker-Kommandos RUN, ENTRYPOINT, CMD, COPY und ADD
WORKDIR /opt/app

# User "nonroot" statt User "root"
USER nonroot

COPY --from=builder --chown=nonroot:nonroot /opt/app ./

# Place executables in the environment at the front of the path
ENV PATH="/opt/app/.venv/bin:$PATH"

EXPOSE 8000

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "-m", "soldat"]
