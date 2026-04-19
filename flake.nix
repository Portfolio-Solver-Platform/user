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

        preCommitCheck = git-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            nixfmt.enable = true;
            trufflehog.enable = true;
            actionlint.enable = true;
            shellcheck.enable = true;
            ruff.enable = true;
            yamllint.enable = true;
            markdownlint = {
              enable = true;
              args = [ "--fix" ];
            };
          };
        };

        ciPackages = with pkgs; [
          pkgs.nodejs_24
          kubernetes-helm
          yq-go
        ];
      in
      {
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
                (python3.withPackages (
                  ps: with ps; [
                    requests
                  ]
                ))
                skaffold
              ]);
          };
        };
      }
    );
}
