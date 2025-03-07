// Copyright 2019-2022 Cambridge Quantum Computing
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include "Utils/GraphHeaders.hpp"

namespace tket {

/**
 * Instance of DirectedGraph to hold dependencies between Qubit UnitID
 * objects as given from some Circuit
 */
class QubitGraph : public graphs::DirectedGraph<Qubit> {
 private:
  using Base = graphs::DirectedGraph<Qubit>;

 public:
  QubitGraph() : Base() {}
  explicit QubitGraph(const qubit_vector_t& _qubits) : Base(_qubits) {}
};

}  // namespace tket
