from base_excitation import base_excitation

class excitation_729(base_excitation):
    #from lattice.scripts.PulseSequences.spectrum_rabi import spectrum_rabi
    from experiment.pulser_sequences.spectrum_rabi import spectrum_rabi
    name = 'Excitation729'
    pulse_sequence = spectrum_rabi
    
if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = excitation_729(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)