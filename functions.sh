set -e 

function run_all_tests {
	python3 -m unittest discover tests
}

function clean {
	rm -rf tests/*.jpg

}

"$@"
