### Steps
1. `docker build . -t imenco-extractor`
2. `docker run --env-file=.env -v $PWD/config:/config imenco-extractor /config/config.yaml`

3. `docker save -o ~/Desktop/imenco-image.tar imenco-extractor`
4. Export to external PC
5. `docker load -i [path_to_tar_file]` (in external PC)
6. Verify installation: `docker images`

