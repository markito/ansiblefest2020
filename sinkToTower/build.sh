#!/bin/sh

s2i build . centos/python-36-centos7 markito/sink2tower:v1 && docker push markito/sink2tower:v1
