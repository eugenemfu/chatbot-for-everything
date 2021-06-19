.PHONY: extract download

MODEL_ZIP_NAME=new_data.tar.gz
MODEL_URL=https://hse-dl-models.s3.eu-central-1.amazonaws.com/$(MODEL_ZIP_NAME)
MODEL_DIR=data/models/new_data


download: $(MODEL_ZIP_NAME)

extract: $(MODEL_ZIP_NAME)
	@mkdir -p $(MODEL_DIR)
	@tar -xvzf $(MODEL_ZIP_NAME) -C $(MODEL_DIR)
	@rm $(MODEL_ZIP_NAME)

$(MODEL_ZIP_NAME):
	wget $(MODEL_URL)
