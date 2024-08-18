{
  description = "Conversion between different music formats";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
        application = mkPoetryApplication { projectDir = ./.; };
      in
      {
        apps.default = { type = "app"; program = "${application}/bin/musicmanager"; };
        devShells.default = pkgs.mkShell { packages = [ pkgs.poetry pkgs.yt-dlp]; };
      });
}
