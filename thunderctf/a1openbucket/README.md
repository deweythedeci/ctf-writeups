# a1openbucket

In this challenge, we are given the following instructions:

`The secret for this level can be found in the Google Cloud Storage (GCS) bucket a1-bucket-...`

(env-tctf) thunderctf66@cloudshell:~/thunder-ctf (disco-bridge-466305-g7)$ gcloud storage ls
gs://a1-bucket-2e7f9c39/
gs://disco-bridge-466305-g7.appspot.com/
gs://gcf-sources-511018413197-us-central1/
gs://staging.disco-bridge-466305-g7.appspot.com/
(env-tctf) thunderctf66@cloudshell:~/thunder-ctf (disco-bridge-466305-g7)$ gcloud storage ls gs://a1-bucket-2e7f9c39
gs://a1-bucket-2e7f9c39/secret.txt
(env-tctf) thunderctf66@cloudshell:~/thunder-ctf (disco-bridge-466305-g7)$ gcloud storage cat gs://a1-bucket-2e7f9c39/secret.txt                                                           
The answer to life, the universe, and everything: 42
(env-tctf) thunderctf66@cloudshell:~/thunder-ctf (disco-bridge-466305-g7)$