# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

rpm:
	rpmbuild --define "_topdir  %(pwd)" \
	--define "_builddir /tmp" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir  %{_topdir}" \
	-ba python-openshift.spec

	mv noarch/*.rpm .

test:
	rpmlint -i *.rpm *.spec

clean:
	rm -rf noarch/ BUILDROOT/

distclean: clean
	rm -f *.rpm

help:
	@echo "Usage: make <target>                                    "
	@echo "                                                        "
	@echo " rpm - create rpm package                               "
	@echo " test - test all packages/spec files with rpmlint       "
	@echo " clean - clean files used to build                      "
	@echo " distclean - execute clean and remove all output files  "
	@echo " help - show this help and exit                         "
