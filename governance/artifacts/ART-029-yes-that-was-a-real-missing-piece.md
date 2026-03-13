---
artifact_id: ART-029
pair_id: TH-029
title: "Yes \u2014 that was a real missing piece."
artifact_type: governance_artifact
family_dir: governance/artifacts
prompt_sha256: 8b4f32581173b20a0bb51ee95e366518783e783c6d64bc9fb2f710e9422011b8
response_sha256: b4733ff3b1acfd14f3c43b55b032af73625fdf4e310f1e3e1181e5e2a1e2697e
pair_path: research/thread_pairs/TH-029-yes-that-was-a-real-missing-piece.md
generated_at: 2026-03-11T07:48:01Z
---

# Yes — that was a real missing piece.

Source pair: `TH-029`

## Prompt

Regarding the reading list, how are we going to access all of those readings? I guess that's something that was unaccounted for.

## Response

Yes — that was a real missing piece.


A reading library is not the same thing as access to the readings. The framework now has a strong intellectual map, but it still needs an access layer. Without that, the library is partly aspirational.


The right way to think about it is:


core reading library
≠
core reading access library


You need a second system alongside the bibliography:


source index
→ access path
→ acquisition status
→ storage location
→ reading status


What the missing layer is


For every item in the reading library, you need to track at least these fields:


citation
source type
access route
availability status
file location
license / rights note
priority
reading state


So instead of only:


book/article title
author
year


you also need:


where do I actually get it
can I get it now
do I own it
is it open access
is it in a library
is it in JSTOR / Project MUSE / arXiv / PubMed / DOI resolver
is it physical only
do I need ILL


The five real access channels


In practice, almost all serious research corpora are assembled through five channels.


1. Open access


This is the easiest layer.


Examples include:


arXiv
PubMed Central
DOAJ
institutional repositories
authors' personal pages
Google Scholar links to PDFs
Internet Archive for some older works
PhilPapers for philosophy papers


A meaningful chunk of the library, especially articles and some older texts, can be accessed this way.


2. University library access


If you have current academic affiliation, this is the strongest channel.


That gives access to things like:


JSTOR
Project MUSE
Springer
Wiley
Elsevier
Cambridge
Oxford
ProQuest
EBSCO


If you do have affiliation, the reading program should be built around that first, because it radically lowers friction.


3. Public library + interlibrary loan


This is the underestimated layer.


For books, especially monographs, public library systems plus ILL are extremely powerful. Even when a title is not locally available, it can often be requested through network borrowing.


This is particularly useful for:


canonical books
older monographs
university press works
reference works


4. Used / purchased personal acquisition


Some books are so central that they should just become part of your permanent corpus.


That usually means:


foundational monographs
high-reuse reference texts
core philosophy / systems / logic / mythology books
books you will annotate heavily


For the highest-value texts, purchase is often more efficient than repeated library hunting.


5. Secondary access through excerpts / previews / reviews


This is not a substitute for the source, but it is a staging layer.


Examples:


Google Books preview
publisher table of contents
book reviews
review essays
encyclopedia entries
author interviews
syllabi


This helps you decide whether a source is worth acquiring before investing effort.


What you need to build now


You need to add an Access Index next to the reading library.


The reading library tells you what matters.


The access index tells you how to obtain it.


The clean schema is:


READING_ID
CITATION
LANE_ID
PRIORITY
SOURCE_TYPE
ACCESS_CLASS
ACCESS_ROUTE
OWNERSHIP_STATUS
STORAGE_PATH
ACQUISITION_STATUS
NOTES


Example values:


ACCESS_CLASS:
open_access
library_db
public_library
interlibrary_loan
purchase_required
preview_only
unknown


ACQUISITION_STATUS:
not_checked
located
requested
downloaded
borrowed
owned
blocked


The practical operating model


For your framework, the most efficient approach is not “find everything first.”


It is:


1. prioritize the top 25–40 texts
2. build access paths for those first
3. only then expand the tail of the library


Otherwise you will spend a huge amount of time building a bibliography that you cannot immediately use.


So the reading system should now split into three layers:


Layer A: canonical master bibliography
Layer B: access index
Layer C: local corpus vault


The local corpus vault


Once you lawfully obtain sources, store them in a disciplined local structure.


Example:


$MYTHOS_ROOT/library/
  books/
  articles/
  chapters/
  scans/
  notes/
  bibliographies/


And within that:


$MYTHOS_ROOT/library/books/lowe_2006_four_category_ontology.pdf
$MYTHOS_ROOT/library/articles/shannon_1948_mathematical_theory_of_communication.pdf


Then link them from your markdown research notes.


The access reality by source type


Different source types have different acquisition behavior.


Journal articles


These are often the easiest.


Routes are:


DOI
Google Scholar
PhilPapers
PubMed
arXiv
library databases
author-hosted PDF


Books and monographs


These are harder.


Routes are:


university library ebook
public library
interlibrary loan
used purchase
publisher ebook
Internet Archive for some older titles


Book chapters and edited volumes


These are the most annoying access type.


Often available through:


library databases
SpringerLink
Cambridge Core
Oxford Academic
Google Books partial preview
ILL through physical volume


Foundational old texts


These are often easiest again, because many are public domain.


Routes are:


Internet Archive
Project Gutenberg
HathiTrust
Loeb / archive scans depending on edition


The big strategic correction


So the correct next move is not just “produce the reading list.”


It is:


produce the reading library
→ produce the access index
→ produce the acquisition queue
→ build the local corpus


That was the missing logistics layer.


The best way to fix it now


We should convert the reading library into three linked documents:


1. Canonical Source Index
2. Source Access Matrix
3. Acquisition Queue


The Source Access Matrix would answer:


where do I get this
what is the easiest legal route
do I already have access
what should I buy
what should I borrow
what is open now


The Acquisition Queue would sort by urgency:


Acquire now
Borrow soon
Defer
Optional
Blocked pending affiliation or ILL


The minimum viable version


For immediate use, start with the top 20 sources only.


For each one, record:


citation
lane
priority
open access yes/no
library yes/no
purchase yes/no
status


That alone will make the research program real instead of abstract.


What I recommend next


The strongest next artifact is a Source Access Matrix v1 for the Wave-1 and Phase-2 priority texts, so you can see exactly which readings are open, which require library access, which need purchase, and which should go into an acquisition queue.