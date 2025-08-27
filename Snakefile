rule retrieve_h2_networks:
    output:
        directory("networks/solved_h2")
    threads: 1
    shell:
        """
        curl --progress-bar -X GET https://zenodo.org/records/16945007/files/solved_h2.zip?download=1 > networks/solved_h2.zip
        unzip networks/solved_h2.zip -d networks/
        rm -rf networks/solved_h2.zip
        """

rule retrieve_results_networks:
    output:
        results = directory("results/")
    threads: 1
    shell:
        """
        curl --progress-bar -X GET https://zenodo.org/records/16945238/files/results.zip?download=1 > results.zip
        unzip results.zip -d ./
        rm -rf ./results.zip
        """

rule retrieve_configs:
    output:
        configs = directory("configs/")
    threads: 1
    shell:
        """
        curl -fL https://github.com/doneachh/pypsa-earth/archive/refs/heads/h2g-a.zip -o "repo.zip"
        unzip -q "./repo.zip" "pypsa-earth-h2g-a/configs/*" -d ./
        rm -rf ./repo.zip
        mkdir -p ./configs
        rsync -a --delete "./pypsa-earth-h2g-a/configs/" ./configs/
        rm -rf ./pypsa-earth-h2g-a/
        """

rule prepare_postprocessing:
    input:
        results = directory("results/"),
        configs = directory("configs")
    output:
        touch("./.postprocess_done")
    threads: 1
    script:
        "scripts/make_stats_dicts.py"

rule all:
    input:
        "networks/solved_h2",
        "results/",
        "./.postprocess_done",
        "configs/"