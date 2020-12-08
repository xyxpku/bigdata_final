FROM singularities/hadoop:2.8


MAINTAINER Yongxin Xu

# Version
ENV SPARK_VERSION=2.4.0

# Set home
ENV SPARK_HOME=/usr/local/spark-$SPARK_VERSION
#ENV SPARK_TMP=/user/local/


# Install dependencies
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install \
    -yq --no-install-recommends  \
      python python3 \
  && apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& wget https://bootstrap.pypa.io/get-pip.py \
	&& python get-pip.py \
	&& pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy

# Install Spark
RUN mkdir -p "${SPARK_HOME}" \
    && mkdir -p /home/data
COPY spark-$SPARK_VERSION-bin-without-hadoop.tgz /usr/local/
#RUN export ARCHIVE=spark-$SPARK_VERSION-bin-without-hadoop.tgz \
#  && export DOWNLOAD_PATH=dist/spark/spark-$SPARK_VERSION/$ARCHIVE \
#  && curl -sSL https://archive.apache.org/$DOWNLOAD_PATH | \
RUN tar -xvf /usr/local/spark-$SPARK_VERSION-bin-without-hadoop.tgz -C $SPARK_HOME --strip-components 1 \
    && rm -rf /usr/local/spark-$SPARK_VERSION-bin-without-hadoop.tgz
COPY spark-env.sh $SPARK_HOME/conf/spark-env.sh
ENV PATH=$PATH:$SPARK_HOME/bin

# Ports
EXPOSE 4040 6066 7077 8080 8081  8182  8030 8031 8032 8033 8040 8041 8042 8088

# Copy yarn mapred
COPY /confyarn/*.xml $HADOOP_CONF_DIR/
# Copy start script
COPY start-spark /opt/util/bin/start-spark
COPY /data/* /home/data/
RUN chmod 777 /opt/util/bin/start-spark

# Fix environment for other users
RUN echo "export SPARK_HOME=$SPARK_HOME" >> /etc/bash.bashrc \
  && echo 'export PATH=$PATH:$SPARK_HOME/bin'>> /etc/bash.bashrc

# Add deprecated commands
RUN echo '#!/usr/bin/env bash' > /usr/bin/master \
  && echo 'start-spark master' >> /usr/bin/master \
  && chmod +x /usr/bin/master \
  && echo '#!/usr/bin/env bash' > /usr/bin/worker \
  && echo 'start-spark worker $1' >> /usr/bin/worker \
  && chmod +x /usr/bin/worker


