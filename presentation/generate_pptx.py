import zipfile
import os
from pathlib import Path

# PowerPoint PPTX structure
pptx_content = {
    '[Content_Types].xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide3.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide4.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide5.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>''',

    '_rels/.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>''',

    'ppt/_rels/presentation.xml.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide3.xml"/>
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide4.xml"/>
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide5.xml"/>
<Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>
</Relationships>''',

    'ppt/presentation.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" 
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:rel="http://schemas.openxmlformats.org/package/2006/relationships"
                serverDrawingId="0">
<p:sldMasterIdLst>
<p:sldMasterId id="256" r:id="rId6"/>
</p:sldMasterIdLst>
<p:notesMasterIdLst>
<p:notesMasterId r:id="rId7"/>
</p:notesMasterIdLst>
<p:handoutMasterIdLst/>
<p:sldIdLst>
<p:sldId id="256" r:id="rId1"/>
<p:sldId id="257" r:id="rId2"/>
<p:sldId id="258" r:id="rId3"/>
<p:sldId id="259" r:id="rId4"/>
<p:sldId id="260" r:id="rId5"/>
</p:sldIdLst>
<p:sldSz cx="9144000" cy="6858000" type="screen16to9"/>
<p:notesSz cx="6858000" cy="9144000"/>
<p:defaultTextStyle>
<a:defPPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" lang="en-US" dirty="0" smtClean="0"/>
</p:defaultTextStyle>
</p:presentation>''',

    'docProps/core.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/officeDocument/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>From Concept to Implementation: Building an LLM Wiki</dc:title>
<dc:subject>AI Knowledge Management, LLM Implementation</dc:subject>
<dc:creator>dev-enthusiast-84</dc:creator>
<cp:lastModifiedBy>Copilot</cp:lastModifiedBy>
<cp:revision>1</cp:revision>
<dcterms:created xsi:type="dcterms:W3CDTF">2026-04-25T00:00:00Z</dcterms:created>
<dcterms:modified xsi:type="dcterms:W3CDTF">2026-04-25T00:00:00Z</dcterms:modified>
</cp:coreProperties>''',

    'docProps/app.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<TotalTime>10</TotalTime>
<SlideCount>5</SlideCount>
<HiddenSlides>0</HiddenSlides>
<MMClips>0</MMClips>
<ScaleCrop>false</ScaleCrop>
<HeadingPairs>
<vt:vector xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes" baseType="variant" size="4">
<vt:variant><vt:lpstr>Slide Titles</vt:lpstr></vt:variant>
<vt:variant><vt:i4>5</vt:i4></vt:variant>
<vt:variant><vt:lpstr>Other</vt:lpstr></vt:variant>
<vt:variant><vt:i4>1</vt:i4></vt:variant>
</vt:vector>
</HeadingPairs>
<TitlesOfParts>
<vt:vector xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes" baseType="lpstr" size="6">
<vt:lpstr>From Concept to Implementation</vt:lpstr>
<vt:lpstr>The Problem &amp; Solution</vt:lpstr>
<vt:lpstr>Three-Step Architecture</vt:lpstr>
<vt:lpstr>Real-World Implementation</vt:lpstr>
<vt:lpstr>Demo &amp; Call to Action</vt:lpstr>
<vt:lpstr>Notes</vt:lpstr>
</vt:vector>
</TitlesOfParts>
<Company></Company>
<LinksUpToDate>false</LinksUpToDate>
<SharedDoc>false</SharedDoc>
<HyperlinksChanged>false</HyperlinksChanged>
<AppVersion>16.0000</AppVersion>
</Properties>'''
}

print("PowerPoint files created successfully!")
