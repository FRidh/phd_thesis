{ pkgs ? import <nixpkgs> {} }:

let
  fetchTarballFromGitHub = { repo, owner, rev, sha256, name ? "" }:
    fetchTarball {
      url = "https://github.com/${owner}/${repo}/archive/${rev}.tar.gz";
      inherit sha256;
      inherit name;
    };

  python = pkgs.python3;



  packageOverrides = let
    # Set with auraliser and dependencies
    auralisation = (import (fetchTarballFromGitHub {
      owner = "FRidh";
      repo = "auralisation-nix";
      rev = "fd6e6a30e3f6a9a75b5f4bf10b74340353a52ef0";
      sha256 = "1ks54pwzff448nxhyqiajlnhlwb8dnsdm42ymi5ncwm7ynd152jy";
    }){}).stableOverrides;

    # Additional packages/overrides
    overrides = self: super: {
        # Package for loading and saving tabular data with metadata.
        h5store = super.callPackage /home/freddy/Code/libraries/h5store { };

        # Function for creating one-file package modules.
        pythonModule = { src, ... } @attrs:
          let
            filename = (builtins.baseNameOf (builtins.toString src));
          in self.buildPythonPackage ({
            format = "other";
            preferLocalBuild = true;
            inherit src;
            name = filename;
            # We copy the file so we can modify it if we have to.
            unpackPhase = ''
            cp $src ${filename}
            '';
            installPhase = ''
              runHook preInstall
              mkdir -p "$out/${python.sitePackages}"
              cp *.py "$out/${python.sitePackages}/${filename}"
              runHook postInstall
            '';
          } // attrs);

        # Simple module providing function for creating the default/common simulation
        common_simulation = self.pythonModule {
          src = ./common_simulation.py;
          propagatedBuildInputs = [ super.auraliser self.h5store ];
        };
      };

  in (pkgs.lib.composeExtensions auralisation overrides);




in python.override {inherit packageOverrides; }




