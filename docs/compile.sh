#!/bin/bash

rm README.rst
touch README.rst
for i in parts/*; do
  cat $i >> README.rst;
done

rst2html README.rst README.html
