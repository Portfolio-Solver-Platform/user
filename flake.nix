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
            trufflehog.enable = true;
            actionlint.enable = true;
            shellcheck.enable = true;
            ruff.enable = true;
            yamllint = {
              enable = true;
              excludes = yamlExcludeList;
            };
            markdownlint.enable = true;
          };
        };

        ciPackages = with pkgs; [
          pkgs.nodejs_24
          kubernetes-helm
          yq-go
        ];
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
          ci = pkgs.mkShell {
            inherit (preCommitCheck) shellHook;
            packages = ciPackages;
          };

          default = pkgs.mkShell {
            inherit (preCommitCheck) shellHook;
            packages =
              ciPackages
              ++ (with pkgs; [
                kubernetes-helm
                (python3.withPackages (ps: with ps; [ requests ]))
                skaffold
              ]);
          };
        };
      }
    );
}
