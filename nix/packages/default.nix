{ pkgs ? import <nixpkgs> {} }:

let
  fetchTarballFromGitHub = { repo, owner, rev, sha256, name ? "" }:
    fetchTarball {
      url = "https://github.com/${owner}/${repo}/archive/${rev}.tar.gz";
      inherit sha256;
      inherit name;
    };

  python = pkgs.python35;

  packageOverrides = let
    # Set with auraliser and dependencies
    auralisation = (import (fetchTarballFromGitHub {
      owner = "FRidh";
      repo = "auralisation-nix";
      rev = "746685780465d52b94351082dffda993e49f26dd";
      sha256 = "0kri678pyxznkkz6595fll2bqw16v7fjh7m8w9hjyvlhnbq0pwib";
    }){}).stableOverrides;

    # Additional packages/overrides
    overrides = self: super: {
        h5store = super.callPackage /home/freddy/Code/libraries/h5store { };
      };
  in (pkgs.lib.composeExtensions overrides auralisation);

in python.override {inherit packageOverrides; }




