This section defines what each state actually means.
You must treat these meanings as authoritative.

INIT

Meaning
A session exists, but no messages have been analyzed.

Allowed actions

Initialize memory

Store first message

Not allowed

Detection

Replies

Extraction

Engagement

Example

First incoming message arrives.

NORMAL

Meaning
Messages are being observed, but there is no confirmed scam intent.

Allowed actions

Accumulate detection signals

Update counters

Not allowed

Agent replies

Extraction

Engagement

Example

Benign or ambiguous message sequence.

SUSPICIOUS

Meaning
Scam intent has been confirmed analytically, but the agent has not yet engaged.

This is an analysis-only state.

Allowed actions

Transition planning

Prepare agent handoff

Not allowed

Replies

Extraction

Callback

Finalization

Non-example
❌ “Agent replies because scam detected”

AGENT_ENGAGED

Meaning
The autonomous agent has taken control of the conversation.

This is the only state where:

Replies are generated

Engagement metrics increase

Intelligence extraction is allowed

Allowed actions

Generate persona replies

Extract intelligence

Prolong conversation

Not allowed

Callback

Finalization (unless explicitly triggered)

INTEL_READY

Meaning
Engagement is explicitly finalized.

This state represents a decision, not a condition.

Allowed actions

Prepare final payload

Send callback

Not allowed

Further replies

Further extraction

Critical rule
INTEL_READY is reached only by explicit finalization logic.

CALLBACK_SENT

Meaning
The mandatory final callback has been successfully delivered.

Allowed actions

Transition to termination

Not allowed

Second callback

Any further processing

TERMINATED

Meaning
The session lifecycle is complete.

Allowed actions

Ignore further messages

Return safe no-op responses