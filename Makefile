# # Minimal makefile for Sphinx documentation
# #

# # You can set these variables from the command line.
# SPHINXOPTS    =
# SPHINXBUILD   = sphinx-build
# SOURCEDIR     = docs
# BUILDDIR      = docs/_build

build_workflow: 
	@echo 'Building YAML...'
	@pip3 install -r yaml_workflows/requirements.txt
	@cd yaml_workflows; python3 workflow_compiler.py
	@echo 'Build complete!'

# # Put it first so that "make" without argument is like "make help".
# help:
# 	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# .PHONY: help Makefile

# # Catch-all target: route all unknown targets to Sphinx using the new
# # "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
# 	# @(cd ..; \
# 	# scp -i sonarqube.pem -r \
# 	# AI-CI/docs/_build/html \
# 	# ubuntu@ec2-44-196-133-163.compute-1.amazonaws.com:\
# 	# /var/www/)