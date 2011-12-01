# Copyright (c) 2011, Open Technologies Bulgaria, Ltd. <http://otb.bg>
# Author: Alexander Todorov <atodorov@nospam.otb.bg>

version := $(shell python setup.py --version)

github:
	git push -u origin master --tags

tar:
	tar -czvf openshift-$(version).tar.gz README LICENSE setup.py openshift/

rpm: tar
	rpmbuild --define "_topdir  %(pwd)" \
	--define "_builddir /tmp" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir  %{_topdir}" \
	-ba python-openshift.spec

	mv noarch/*.rpm .

release: tar rpm

rpm-test:
	rpmlint -i *.rpm *.spec

sanity-test:
	chmod a+x tests/sanity.sh
	./tests/sanity.sh

unit-test:
	for f in tests/*.py; do python $$f; done

test: sanity-test unit-test

clean:
	rm -rf noarch/ BUILDROOT/
	rm -f openshift/*.pyc
	rm -f tests/*.pyc

distclean: clean
	rm -f *.rpm *.tar.gz

help:
	@echo "Usage: make <target>                                    "
	@echo "                                                        "
	@echo " github - push to GitHub                                "
	@echo " tar - make a tarball                                   "
	@echo " rpm - create rpm package                               "
	@echo " release - build all release files                      "
	@echo " rpm-test - test all packages/spec files with rpmlint   "
	@echo " sanity-test - run all sanity tests                     "
	@echo " unit-test - run all unit tests                         "
	@echo " test - run all available tests                         "
	@echo " clean - clean files used to build                      "
	@echo " distclean - execute clean and remove all output files  "
	@echo " help - show this help and exit                         "
