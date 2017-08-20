let
  # Function to fetch a tarball with Nix expressions from GitHub
  fetchTarballFromGitHub = { repo, owner, rev, sha256, name ? "" }:
    fetchTarball {
      url = "https://github.com/${owner}/${repo}/archive/${rev}.tar.gz";
      inherit sha256;
      inherit name;
    };

  # import <nixpkgs> {}; but from a specific commit.
  pkgs = import (fetchTarballFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev= "afd2bdbad25db4b0007b52d07161345e6426ae72";
    sha256 = "1n47x3y2q6pxncnp9xq7kxvc9p239g1xkp1wzdw2a9sp9hfva65q";
  }){};

  inherit (pkgs) callPackage;
  latex = pkgs.texlive.combined.scheme-full;

in rec {

  # PDF version of the thesis
  thesis = callPackage ./nix/thesis {
    inherit latex thesis-source python;
  };

  # PDF version of thesis announcement
  thesis-announcement = callPackage ./nix/announcement {
    inherit latex thesis-source;
  };

  # Standalone source tree containing everything needed to build the thesis.
  thesis-source = callPackage ./nix/thesis-source {
    inherit references media audio overview-paper;
  };

  overview-paper = callPackage ./nix/overview-paper {
    inherit media audio figures references latex python;
  };

  audio = callPackage ./nix/audio {
    inherit media python;
    inherit (pkgs) zip;
  };

  figures = callPackage ./nix/figures {
    inherit media;
  };

  # Bibtex library with references/citations
#   references = ./data/library.bib; #/home/freddy/Data/Media/References/library.bib;
  references = /home/freddy/Data/Media/References/library.bib;

  data = rec {
    # Tarball with listening test data.
    listening-test-tests = pkgs.fetchurl {
      url = https://zenodo.org/record/376263/files/test.tar.gz;
      sha256 = "1zg9yg794g3wk2kqv259134hlkd5rwqib8zvlvwz70589cc1pism";
    };
    # CSV text file with listening test results
    listening-test-results = pkgs.fetchurl {
      url = https://zenodo.org/record/376268/files/results.csv;
      sha256 = "0f32451gcr2ikxcb7qwj28q6m7rq148s6vic14j66b1g3hnh7vv8";
    };
  };

  # Media: figures and audio
  media = rec {
    # Step-by-step add propagation effects
    propagation = callPackage ./nix/media/propagation {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    # Basic sound, impedance, reflection, attenuation
    sound = callPackage ./nix/media/sound {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    # Basic sound, Lloyd's mirror effect.
    sound-mirror-effect = callPackage ./nix/media/sound-mirror-effect {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
    # Signal processing. Convolution.
    signal-processing = callPackage ./nix/media/signal-processing {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    # Signal processing. Comparison interpolation methods.
    signal-processing-resampling = callPackage ./nix/media/signal-processing-resampling {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
    # Chapter 5. Turbulence and a pure tone.
    turbulence-tone = callPackage ./nix/media/turbulence-tone {
      inherit python;
      inherit (lib) matplotlibHook;
    };
    turbulence-parameters = callPackage ./nix/media/turbulence-parameters {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
    # Distant source with aircraft-like spectrum. Atmospheric turbulence.
    propagation-distant = callPackage ./nix/media/propagation-distant {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
    # From recording to auralisation. Samples from second paper.
    recording-to-auralisation = callPackage ./nix/media/recording-to-auralisation {
      inherit python;
      inherit (lib) matplotlibHook to_wav;
    };
    # Listening test data
    listening = callPackage ./nix/media/listening {
      inherit python;
      inherit (lib) matplotlibHook;
      inherit (data) listening-test-tests;
    };
    listening-analysis = callPackage ./nix/media/listening-analysis {
      inherit python;
      inherit (lib) matplotlibHook;
      inherit (data) listening-test-tests listening-test-results;
    };
  };

  # Library of functions
  lib = callPackage ./nix/lib {
    inherit python;
  };

  # Python interpreter that has extra packages available
  python = callPackage ./nix/packages { };

  # Papers that are appended to the thesis
  papers = {
    overview = ./data/papers/overview.pdf;
    turbulence = ./data/papers/turbulence.pdf;
  };
}
