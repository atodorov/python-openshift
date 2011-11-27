# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

github:
	git push -u origin master --tags

rpm:
	rpmbuild --define "_topdir  %(pwd)" \
	--define "_builddir /tmp" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir  %{_topdir}" \
	-ba python-openshift.spec

	mv noarch/*.rpm .

rpm-test:
	rpmlint -i *.rpm *.spec

sanity-test:
	pylint -E src/*.py
	pylint -E tests/*.py

unit-test:
	for f in tests/*.py; do python $$f; done

test: sanity-test unit-test

clean:
	rm -rf noarch/ BUILDROOT/

distclean: clean
	rm -f *.rpm

help:
	@echo "Usage: make <target>                                    "
	@echo "                                                        "
	@echo " github - push to GitHub                                "
	@echo " rpm - create rpm package                               "
	@echo " rpm-test - test all packages/spec files with rpmlint   "
	@echo " sanity-test - run all sanity tests                     "
	@echo " unit-test - run all unit tests                         "
	@echo " test - run all available tests                         "
	@echo " clean - clean files used to build                      "
	@echo " distclean - execute clean and remove all output files  "
	@echo " help - show this help and exit                         "
