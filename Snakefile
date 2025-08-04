rule retrieve_h2_networks:
    output:
        directory("networks/solved_h2")
    threads: 1
    shell:
        """
        gdown --folder https://drive.google.com/drive/folders/13YUrD8ZkR29UUivwwlqyLfmNWMmzdQsx
        mkdir -p networks/solved_h2
        cd "SolvedH2"
        mv * ../networks/solved_h2/
        cd ..
        rm -r "SolvedH2"
        """