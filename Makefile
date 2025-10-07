.PHONY: tf-clean tf-init tf-plan tf-apply tf-destroy

tf-clean:
	cd deploy/terraform && \
	rm -rf .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup

tf-init:
	cd deploy/terraform && \
	terraform init

tf-plan:
	cd deploy/terraform && \
	terraform init && \
	terraform plan

tf-apply:
	cd deploy/terraform && \
	terraform init && \
	terraform apply -auto-approve

tf-destroy:
	cd deploy/terraform && \
	terraform init && \
	terraform destroy -auto-approve