TEST = pytest 
TEST_ARGS = --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8 --ignore=E501,C901
STYLE_FIX = autopep8 --in-place --recursive --aggressive --aggressive

.PHONY: all
all: clean run-test
#style-check type-check
.PHONY: type-check
type-check:
	$(TYPE_CHECK) .

.PHONY: style-check
style-check:
	$(STYLE_CHECK) .

# discover and run all tests
.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) .

.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .hypothesis


.PHONY: push
push: run-test clean
	

.PHONY: fix-style
fix-style:
	$(STYLE_FIX) .
