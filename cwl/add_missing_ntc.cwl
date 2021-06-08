$namespaces:
  edam: http://edamontology.org/
  s: https://schema.org/
baseCommand:
- add_missing_ntc.py
class: CommandLineTool
cwlVersion: v1.0
hints:
  DockerRequirement:
    dockerPull: docker.io/sagebionetworks/dockstore-tool-add_missing_ntc:0.0.1
inputs:
  count_file:
    inputBinding:
      prefix: --file
    type: File
  reference_file:
    inputBinding:
      prefix: --reference
    type: File
label: Add missing NTC rows according to NTC family and existing higest freq
outputs:
  output_file:
    outputBinding:
      glob: $(inputs.count_file.basename)_add_ntc.txt
    type: File
s:author:
- class: s:Person
  s:email: xindi.guo@sagebase.org
  s:identifier: https://orcid.org/0000-0002-0479-4317
  s:name: Xindi Guo
s:license: https://spdx.org/licenses/Apache-2.0
