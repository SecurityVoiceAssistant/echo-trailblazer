FROM kalilinux/kali-rolling

# install kali packages
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y full-upgrade
RUN apt-get -y install ca-certificates
RUN apt-get -y install kali-linux-core kali-system-cli
RUN apt-get -y install theharvester libimage-exiftool-perl exploitdb 
RUN apt-get clean

# install conda
ENV PATH=/opt/conda/bin:$PATH
ARG CONDA_VERSION=py311_24.1.2-0

RUN mkdir -p /opt/conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh -q
RUN bash ~/miniconda.sh -b -u -p /opt/conda
RUN rm ~/miniconda.sh
RUN conda update conda -y

# create user
ARG USER=et_dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV HOME=/home/$USER

RUN groupadd -r --gid $USER_GID $USER
RUN useradd -r --uid $USER_UID --gid $USER_GID -g $USER -m -s /bin/zsh $USER
RUN echo $USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER
RUN chmod 0440 /etc/sudoers.d/$USER
RUN chown -R $USER:$USER /opt/conda
USER $USER

# app setup
WORKDIR $HOME/app
RUN chown -R $USER:$USER $HOME/app
COPY . .
RUN conda env create -n et -f environment.yml

EXPOSE 22
EXPOSE 443

SHELL ["/bin/zsh", "-c"]
CMD ["conda", "run", "--no-capture-output", "-n", "et", "python", "src/main.py"]

