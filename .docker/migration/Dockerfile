FROM dimitri/pgloader:ccl.latest

# Switch to root to install packages
USER root

# Install comprehensive locale and encoding support
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    locales-all \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Add CP1250 and related Central European locales
RUN echo "cs_CZ.CP1250 CP1250" >> /etc/locale.gen && \
    echo "sk_SK.CP1250 CP1250" >> /etc/locale.gen && \
    echo "pl_PL.CP1250 CP1250" >> /etc/locale.gen && \
    echo "hu_HU.CP1250 CP1250" >> /etc/locale.gen && \
    locale-gen

# Set environment to support the encoding
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Don't switch users - the base image runs as root
