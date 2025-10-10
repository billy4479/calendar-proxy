{
  description = "Calendar Proxy";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPkgs = pkgs.python3.withPackages (
          python-pkgs:
          (with python-pkgs; [
            ics
            requests
            python-dotenv
            flask
            gunicorn
          ])
        );
      in
      {
        packages = rec {
          files = pkgs.stdenvNoCC.mkDerivation {
            pname = "calendar-proxy";
            version = "1.0.0";

            src = ./.;
            dontBuild = true;
            dontCondigure = true;
            dontFixup = true;

            installPhase = # sh
              ''
                mkdir -p $out
                mv *.py $out
              '';
          };

          container = pkgs.dockerTools.buildLayeredImage {
            name = "calendar-proxy";
            tag = "latest";

            contents = [
              pythonPkgs
              files
            ];

            config = {
              Cmd = [
                "gunicorn"
                "--chdir"
                "${files}"
                "app:app"
              ];
            };
          };
        };
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            pythonPkgs
            ruff
            basedpyright
          ];
        };
      }
    );
}
