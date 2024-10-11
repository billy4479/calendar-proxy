{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            nodejs_latest
            nodePackages_latest.vercel

            (python3.withPackages (
              python-pkgs:
              (with python-pkgs; [
                ics
                requests
                python-dotenv
                flask
              ])
            ))

            ruff
          ];
        };
      }
    );
}
