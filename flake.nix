{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      git-hooks,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        yamlExcludeList = [
          "^helm/templates/"
          "^.git/"
          "^.github/"
        ];

        preCommitCheck = git-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            nixfmt.enable = true;
            check-merge-conflicts.enable = true;
            hadolint.enable = true; # Dockerfile linting
            trufflehog.enable = true;
            actionlint.enable = true;
            shellcheck.enable = true;
            ruff.enable = true;
            yamllint = {
              enable = true;
              excludes = yamlExcludeList;
            };
            markdownlint.enable = true;

            helm-lint = {
              enable = true;
              name = "Helm Lint";
              pass_filenames = false;
              entry =
                let
                  packages = with pkgs; [
                    kubernetes-helm
                  ];

                  wrapper = pkgs.writeShellScript "helm-lint-wrapper" ''
                    export PATH="${pkgs.lib.makeBinPath packages}:$PATH"

                    exec ${pkgs.bash}/bin/bash -c "helm lint ./helm/"
                  '';
                in
                builtins.toString wrapper;
            };
          };
        };
      in
      {
        formatter = pkgs.writeShellScriptBin "format-all" ''
          echo "=== Formatting Nix files... ==="
          find . -type f -name "*.nix" -exec ${pkgs.nixfmt}/bin/nixfmt {} +

          echo "=== Formatting Markdown files... ==="
          ${pkgs.markdownlint}/bin/markdownlint --fix .

          echo ""
          echo "=== Done! ==="
        '';

        devShells = {
          default = pkgs.mkShell {
            inherit (preCommitCheck) shellHook;
            packages = with pkgs; [
              kubernetes-helm
              (python3.withPackages (ps: with ps; [ requests ]))
              skaffold
              uv
            ];
          };

          checks = pkgs.mkShell {
            inherit (preCommitCheck) shellHook;
          };

          release = pkgs.mkShell {
            packages = with pkgs; [
              pkgs.nodejs_24
              kubernetes-helm
              yq-go
              jq
            ];
          };
        };
      }
    );
}
