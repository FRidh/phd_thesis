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
      rev = "7a3b2694d5cbb0aaccf3d0d6aca5c174de32d060";
      sha256 = "0kb5l5j5dbpj490ny9jc8nbr60lra84c6p2f5xxg0s876prrplwd";
    }){}).stableOverrides;

    # Additional packages/overrides
    overrides = self: super: {
        h5store = super.callPackage /home/freddy/Code/libraries/h5store { };
      };
  in (pkgs.lib.composeExtensions overrides auralisation);

in python.override {inherit packageOverrides; }




