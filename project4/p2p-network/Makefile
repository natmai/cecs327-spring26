NETWORK      = p2p-net
NUM_NODES    = 50
MSG_COUNT    = 15

# ── Setup ──────────────────────────────────────────────────────────────────

network:
	docker network create $(NETWORK) 2>/dev/null || true

build: network
	docker build -t p2p-node .
	docker build -t bootstrap-node -f bootstrap.Dockerfile .

# ── Run ────────────────────────────────────────────────────────────────────

bootstrap: build
	docker run -d --name bootstrap --network $(NETWORK) -p 5050:5000 bootstrap-node

nodes: bootstrap
	@for i in $$(seq 1 $(NUM_NODES)); do \
		PORT=$$((5000 + i)); \
		docker run -d --name node$$i --network $(NETWORK) \
			-p $$PORT:5000 \
			-e NODE_PORT=$$PORT \
			-e NODE_URL="http://node$$i:5000" \
			-e BOOTSTRAP_URL="http://bootstrap:5000" \
			p2p-node; \
	done
	@echo "Started $(NUM_NODES) nodes."

# ── Test ───────────────────────────────────────────────────────────────────

test-peers:
	curl -s http://localhost:5050/peers | python3 -m json.tool

test-messages:
	@for i in $$(seq 1 $(MSG_COUNT)); do \
		SRC=$$((( RANDOM % $(NUM_NODES) ) + 1)); \
		DST=$$((( RANDOM % $(NUM_NODES) ) + 1)); \
		SRC_PORT=$$((5000 + SRC)); \
		DST_PORT=$$((5000 + DST)); \
		echo "Sending from node$$SRC to node$$DST"; \
		curl -s -X POST http://localhost:$$DST_PORT/message \
			-H "Content-Type: application/json" \
			-d "{\"sender\": \"node$$SRC\", \"msg\": \"Hello node$$DST from node$$SRC!\"}"; \
		echo ""; \
	done

# ── Cleanup ────────────────────────────────────────────────────────────────

stop:
	@docker stop bootstrap 2>/dev/null || true
	@for i in $$(seq 1 $(NUM_NODES)); do \
		docker stop node$$i 2>/dev/null || true; \
	done

clean: stop
	@docker rm bootstrap 2>/dev/null || true
	@for i in $$(seq 1 $(NUM_NODES)); do \
		docker rm node$$i 2>/dev/null || true; \
	done
	docker network rm $(NETWORK) 2>/dev/null || true

# ── All-in-one ─────────────────────────────────────────────────────────────

all: nodes
	@echo "Waiting 5 seconds for nodes to register..."
	@sleep 5
	@$(MAKE) test-peers
	@$(MAKE) test-messages