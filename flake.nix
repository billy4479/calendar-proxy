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
        packages.default = pkgs.stdenvNoCC.mkDerivation {
          pname = "calendar-proxy";
          version = "1.0.0";

          src = ./.;
          dontBuild = true;
          dontConfigure = true;

          nativeBuildInputs = [ pkgs.makeWrapper ];

          installPhase = ''
            mkdir -p $out/bin $out/share/calendar-proxy
            cp *.py $out/share/calendar-proxy/

            makeWrapper ${pythonPkgs}/bin/gunicorn $out/bin/calendar-proxy \
              --prefix PYTHONPATH : "$out/share/calendar-proxy" \
              --add-flags "app:app --access-logfile -"
          '';
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
