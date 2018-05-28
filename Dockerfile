FROM gw000/keras

WORKDIR /opt/forecaster/ 

RUN pip install \
      pandas \
      pandas-gbq \
      google-cloud-pubsub \
      sklearn

ENV TF_CPP_MIN_LOG_LEVEL 2
ENV GOOGLE_APPLICATION_CREDENTIALS /opt/forecaster/key.json

ADD src/ queries model.h5 scaler.save \
      ./

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["service.py"]
