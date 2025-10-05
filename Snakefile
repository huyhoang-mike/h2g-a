rule retrieve_h2_networks:
    output:
        directory("networks/solved_h2")
    threads: 1
    shell:
        """
        mkdir -p networks
        curl --progress-bar -X GET https://zenodo.org/records/16945007/files/solved_h2.zip?download=1 > networks/solved_h2.zip
        unzip networks/solved_h2.zip -d networks/
        rm -rf networks/solved_h2.zip
        """

rule retrieve_AP2_results_networks:
    output:
        touch(".AP2_results_done")
    threads: 1
    shell:
        """
        set -e
        mkdir -p results
        curl -fL --progress-bar https://zenodo.org/records/17129490/files/AP2_pypsa_earth_results.zip?download=1 -o AP2_pypsa_earth_results.zip 
        unzip -q AP2_pypsa_earth_results.zip -d results
        mv results/AP2_pypsa_earth_results/* results/ || true
        rm -rf AP2_pypsa_earth_results.zip results/AP2_pypsa_earth_results
        """

rule retrieve_configs:
    output:
        configs = directory("configs/")
    threads: 1
    shell:
        """
        curl -fL --progress-bar https://github.com/doneachh/pypsa-earth/archive/refs/heads/h2g-a.zip -o "repo.zip"
        unzip -q "./repo.zip" "pypsa-earth-h2g-a/configs/*" -d ./
        rm -rf ./repo.zip
        mkdir -p ./configs
        rsync -a --delete "./pypsa-earth-h2g-a/configs/" ./configs/
        rm -rf ./pypsa-earth-h2g-a/
        """

rule prepare_postprocessing:
    input:
        ".AP2_results_done",
        configs = directory("configs")
    output:
        touch(".postprocess_done")
    threads: 1
    script:
        "scripts/make_stats_dicts.py"

rule all:
    input:
        "networks/solved_h2",
        ".AP2_results_done",
        ".postprocess_done"