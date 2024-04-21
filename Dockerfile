FROM kalilinux/kali-rolling

# kali-linux setup
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y dist-upgrade && \
    apt-get -y autoremove && \
    apt-get clean

RUN apt-get -y install ca-certificates && \
    apt-get -y install kali-linux-core kali-system-cli
RUN apt-get -y install theharvester libimage-exiftool-perl exploitdb

# conda setup
ENV PATH=/opt/conda/bin:${PATH}
ARG CONDA_VERSION=py311_24.1.2-0

RUN mkdir -p /opt/conda && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh -q && \
    bash ~/miniconda.sh -b -u -p /opt/conda && \
    rm ~/miniconda.sh && \
    conda update conda -y

# user setup
ARG USER=et_dev
ARG USER_UID=1000
ARG USER_GID=${USER_UID}
ENV HOME=/home/${USER}

RUN groupadd -r --gid ${USER_GID} ${USER} && \
    useradd -r --uid ${USER_UID} --gid ${USER_GID} -g ${USER} -m -s /bin/zsh ${USER} && \
    echo ${USER} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER} && \
    chmod 0440 /etc/sudoers.d/${USER}

RUN chown -R ${USER}:${USER} /opt/

USER ${USER}

# app setup
WORKDIR ${HOME}/echo-trailblazer

COPY --chown=${USER}:${USER} . .
RUN conda env create -n et -f environment.yml

# entrypoint
EXPOSE 80 443 22
SHELL ["/bin/zsh", "-c"]
CMD ["conda", "run", "--no-capture-output", "-n", "et", "python", "src/main.py"]

